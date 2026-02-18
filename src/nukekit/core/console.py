import logging
from typing import Any, Literal, get_args, get_origin

from rich import print
from rich.tree import Tree
from simple_term_menu import TerminalMenu

from .assets import Asset
from .serialization import stringify_keys

logger = logging.getLogger(__name__)

RETURN_TYPES = Literal["bool", "str"]


def choose_menu(d: dict, level_name: str = "Main menu") -> Asset:
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
        raise TypeError(f"Provided asset is not of type {Asset}")

    else:
        logger.info("Asset install aborted.")
        quit()


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
