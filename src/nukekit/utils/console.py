import logging

from simple_term_menu import TerminalMenu
from rich import print
from rich.tree import Tree

from ..core.assets import Asset

logger = logging.getLogger(__name__)


def choose_menu(d:dict, level_name:str = "Main menu")->Asset:
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
        options.append('Return')
        terminal_menu = TerminalMenu(options, title= level_name)
        menu_entry_index = terminal_menu.show()

        if options[menu_entry_index] == 'Return':
            break
        try: 
            key = options[menu_entry_index]
            value = d[key]
        except (ValueError, IndexError):
            print('Invalid selection')
        else:
            if isinstance(value, Asset):
                return value
            elif isinstance(value, dict):
                value = choose_menu(value, level_name=key)
        if value is not None:
            return value
    if value is not None:
        return value

def print_data(data:dict, label:str = 'Manifest'):
    """
    Print input dictionnary as tree in terminal 
    
    :param data: Data to displauy
    :type data: dict
    :param label: Top level label for this branch of the tree 
    :type label: str
    """
    
    format_string = "| {:<12} | {:<8} | {:<10} |"
    
    def recursive_tree(d:dict, t:Tree):
        for key, value in d.items():
            if key == 'latest_version':
                continue
            if key == "versions":
                t.add(format_string.format("Status", "Version", "Id" ))
                for v in value.values():
                    t.add(format_string.format(str(v.status.name), str(v.version),str(v.id)))
                break
            sub_tree = t.add(key)
            if isinstance(value, dict):
                recursive_tree(value, sub_tree)

    # Initilize tree 
    tree = Tree(label)
    
    # Loop through asset categories and create a tree from recursive exploration
    for category, assets_dict in data.items():
        category_tree = tree.add(category)
        recursive_tree(assets_dict, category_tree)

    print(tree)
    