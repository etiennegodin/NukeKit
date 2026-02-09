from __future__ import annotations
import shutil
import logging

from .assets import Asset
from .context import Context

logger = logging.getLogger(__name__)

class Installer():
    def __init__(self, context:Context):
        self.context = context

    def install_all(self):
        raise NotImplementedError('Not implemented')
        pass

    def install_from_repo(self):
        raise NotImplementedError('Not implemented')

        logger.debug('Install from repo')
        assets = self.context.repo_manifest.read_manifest()

        print('installer')
        #print(assets)
        #print_json(json.dumps(assets,cls=UniversalEncoder))
        
        asset = assets['Gizmo']['city']['versions']['0.1.0']
        self.install_asset(asset)

    def install_asset(self, asset:Asset):
        #Force back type if read from string 
        source_path = asset.get_remote_path(self.context.repo)
        destination_path = self.context.user_paths.NUKE_KIT_DIR

        try:
            shutil.copy2(source_path, destination_path)
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            asset.set_install_status('local')
            self.context.local_manifest.update(asset)
            return True
        