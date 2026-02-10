import logging

from rich import print
from rich.tree import Tree
from simple_term_menu import TerminalMenu
from typing import Literal, get_args, get_origin, Any, TYPE_CHECKING

from ..core.assets import Asset

logger = logging.getLogger(__name__)

RETURN_TYPES = Literal["bool", "str"]

def choose_menu(d:dict, level_name:str = "Main menu") -> Asset:
    """
    Interactive terminal selection menu    

    :param d: Data to explore 
    :type d: dict
    :param level_name: Name for menu/sub-menu
    :type level_name: str
    :return: Asset instance from selected option
    :rtype: Asset
    """
    value = None
    while True:
        options = list(d.keys())
        options.append("Return")
        terminal_menu = TerminalMenu(options, title= level_name)
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
        return value

def print_data(data:dict, label:str = "Manifest"):
    """
    Print input dictionnary as tree in terminal 
    
    :param data: Data to displauy
    :type data: dict
    :param label: Top level label for this branch of the tree 
    :type label: str
    """
    
    format_string = "| {:<12} | {:<8} | {:<10} |"
    
    def recursive_tree(d:dict, t:Tree, stop:str):
        for key, value in d.items():
            if key == stop:
                t.add(format_string.format("Status", "Version", "Id" ))
                for v in value.values():
                    t.add(format_string.format(v.status.name, v.version, str(v.id)))
                break
            sub_tree = t.add(key)
            if isinstance(value, dict):
                recursive_tree(value, sub_tree)

    # Initilize tree 
    tree = Tree(label)
    
    # Loop through asset categories and create a tree from recursive exploration
    for category, assets_dict in data.items():
        category_tree = tree.add(category)
        for asset_name, asset_data in assets_dict.items():
            asset_tree = tree.add(asset_name)
            recursive_tree(assets_dict, asset_tree, asset_name)

    print(tree)


def _add_question_mark(question:str)->str:
    if not question.endswith("?"):
        question += "?"
    return question

def _format_options_list(options:Any):
    if get_origin(options) is Literal:
        options = list(get_args(options))
    return options

def user_input_choice(question:str, options:list[str] = ["y","n"], type:RETURN_TYPES = "bool")-> bool | str:
    """
    Ask user a question with options answers in terminal. Loops until correct answer is given.

    :param question: Question to ask
    :type question: str
    :param options: Options of correct answers. Defaults to y/n
    :type options: list[str]
    :param type: Type of return, either string or bool. Defaults to bool.
    :type type: RETURN_TYPES
    :return: Returns bool if y/n, str from options
    :rtype: bool | str
    """
    correct = False
    question = _add_question_mark(question)
    options = _format_options_list(options)

    while not correct:
        user_input_choice = input(f"{question} {[o for o in options]} ")
        if user_input_choice in options:
            correct = True
        else:
            print("\033[1A\033[K", end="") 

    if type == "bool":
        return user_input_choice == "y"
    return user_input_choice

    