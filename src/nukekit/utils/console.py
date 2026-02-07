from rich import print
from rich.table import Table
from rich.console import Console
from rich.tree import Tree
from ..core.assets import AssetStatus


def menu2():
    from pick import pick

    title = 'Please choose a file:'
    options = ['file1.txt', 'file2.txt', '\t/file3.txt']
    option, index = pick(options, title)
    print(f"Selected: {option} - {index}")

def menu():
    
    from simple_term_menu import TerminalMenu

    options = ["Option 1", "Option 2", "Option 3"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You selected: {options[menu_entry_index]}")


def print_manifest(manifest:dict, status_filter:AssetStatus = None):
    def recursive_tree(d:dict, t:Tree):
        for key, value in d.items():
            if key == 'latest_version':
                continue
            if key == "versions":
                for v in value.values():
                    if v.status == status_filter:
                        t.add(f"{str(v.version)} - {v.id}")
                break
            sub_tree = t.add(key)
            if isinstance(value, dict):
                recursive_tree(value, sub_tree)

    tree = Tree('Manifest')

    for category, assets_dict in manifest.items():
        category_tree = tree.add(category)
        recursive_tree(assets_dict, category_tree)
    print(tree)
    