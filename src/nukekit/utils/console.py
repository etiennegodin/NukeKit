import logging
from rich import print
from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from ..core.assets import AssetStatus, Asset
from simple_term_menu import TerminalMenu

logger = logging.getLogger(__name__)


def menu2(options:dict):
    from pick import pick

    title = 'Please choose a file:'
    #options = ['file1.txt', 'file2.txt', '\t/file3.txt']
    option, index = pick(options, title)
    print(f"Selected: {option} - {index}")

def choose_menu(d:dict, level_name = "Main menu")->Asset:
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
            return value
    return value

def print_manifest(manifest:dict, label = 'Manifest'):
    format_string = "| {:<12} | {:^8} | {:^8} |"
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

    tree = Tree(label)

    for category, assets_dict in manifest.items():
        category_tree = tree.add(category)
        recursive_tree(assets_dict, category_tree)

    print(tree)
    