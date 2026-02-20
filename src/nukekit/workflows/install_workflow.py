"""
Install workflow with dependency injection.

This is pure business logic - no I/O creation, no error handling.
The ApplicationService handles those concerns.
"""

import logging

from ..app.container import Dependencies
from ..core import ManifestStore, console, copy
from ..core.exceptions import UserAbortedError

logger = logging.getLogger(__name__)


def execute(deps: Dependencies, interactive: bool = True) -> dict:
    """
    Execute install workflow.

    Args:
        deps: Injected dependencies
        interactive: If True, prompt user for asset selection

    Returns:
        dict with 'asset' key

    Raises:
        UserAbortedError: If user cancels
    """
    if deps.repo_manifest is None or deps.cached_manifest is None:
        raise ValueError("Manifests not loaded")

    # User chooses asset from repository manifest
    if interactive:
        console.print_data(deps.repo_manifest.to_dict())
        asset = console.choose_asset_fzf(deps.repo_manifest.to_dict(), prompt="Install")
        if asset is None:
            raise UserAbortedError("User cancelled asset selection")
    else:
        raise NotImplementedError("Non-interactive install not yet supported")

    # Install locally
    copy.copy_asset(
        deps.repository.get_asset_path(asset),
        deps.user_paths.NUKE_KIT_DIR / asset.get_file_name(),
    )
    asset.set_install_status("local")

    # Update local manifest and save
    deps.cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(deps.cached_manifest, deps.user_paths.CACHED_MANIFEST)

    return {"asset": asset}
