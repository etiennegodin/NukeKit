import logging
from typing import Any, Literal, get_args, get_origin

from InquirerPy import inquirer
from rich import print
from rich.tree import Tree
from simple_term_menu import TerminalMenu

from .assets import Asset
from .exceptions import InvalidAssetError
from .serialization import stringify_keys
from .versioning import Version

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


def _unique_asset_names(
    data: dict,
) -> list[tuple[str, tuple[Any, str]]]:
    """List unique (type, name) from manifest data.
    Returns (display, (type_key, name))."""
    seen: set[tuple[Any, str]] = set()
    result: list[tuple[str, tuple[Any, str]]] = []
    for type_key, names in data.items():
        type_str = getattr(type_key, "value", type_key) if type_key else ""
        for name in names:
            key = (type_key, name)
            if key not in seen:
                seen.add(key)
                result.append((f"[{type_str}] {name}", key))
    return result


def _version_choices_for_asset(
    data: dict, type_key: Any, name: str
) -> list[tuple[str, Asset]]:
    """Build (display, Asset) list for one asset: Latest (x.y.z) + each version."""
    version_dict = data[type_key][name]
    if not version_dict:
        return []
    version_keys = list(version_dict.keys())
    latest = Version.highest_version(version_keys)
    # Resolve Asset for latest (key might be Version or str)
    latest_asset = next(
        (version_dict[k] for k in version_dict if str(k) == str(latest)),
        next(iter(version_dict.values())),
    )

    def _version_sort_key(v: Any) -> tuple[int, int, int]:
        if hasattr(v, "major"):
            return (v.major, v.minor, v.patch)
        try:
            ver = Version.from_string(str(v))
            return (ver.major, ver.minor, ver.patch)
        except (ValueError, TypeError):
            return (0, 0, 0)

    sorted_versions = sorted(version_dict.keys(), key=_version_sort_key, reverse=True)
    choices: list[tuple[str, Asset]] = [
        (f"Latest ({latest})", latest_asset),
    ]
    for v in sorted_versions:
        choices.append((str(v), version_dict[v]))
    return choices


def choose_asset_fuzzy(
    manifest_data: dict,
    prompt: str = "Select asset",
    prompt_version: str = "Version to install",
) -> Asset | None:
    """
    Two-step picker: choose asset (name) then version (Latest or specific).

    Step 1: Fuzzy list of unique asset names [Type] Name.
    Step 2: Fuzzy list "Latest (x.y.z)" plus each available version.

    Args:
        manifest_data: Nested dict from Manifest.to_dict()
        (type -> name -> version -> Asset).
        prompt: Prompt for the asset step.
        prompt_version: Prompt for the version step (e.g. "Version to install").

    Returns:
        Selected Asset, or None if user aborted.
    """
    asset_choices = _unique_asset_names(manifest_data)
    if not asset_choices:
        return None

    display_list = [display for display, _ in asset_choices]
    try:
        selected_display = inquirer.fuzzy(
            message=prompt,
            choices=display_list,
        ).execute()
    except (KeyboardInterrupt, EOFError):
        return None

    if not selected_display:
        return None

    type_key, name = next(
        (key for display, key in asset_choices if display == selected_display),
        (None, None),
    )
    if type_key is None or name is None:
        return None

    version_choices = _version_choices_for_asset(manifest_data, type_key, name)
    if not version_choices:
        return None
    if len(version_choices) == 1:
        return version_choices[0][1]

    version_display_list = [display for display, _ in version_choices]
    try:
        selected_version_display = inquirer.fuzzy(
            message=prompt_version,
            choices=version_display_list,
        ).execute()
    except (KeyboardInterrupt, EOFError):
        return None

    if not selected_version_display:
        return None
    for display, asset in version_choices:
        if display == selected_version_display:
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
