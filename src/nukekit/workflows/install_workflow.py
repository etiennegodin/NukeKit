"""
Install workflow with dependency injection.

This is pure business logic - no I/O creation, no error handling.
The ApplicationService handles those concerns.
"""

import logging

from ..app.container import Dependencies
from ..core import ManifestStore, console, copy
from ..core.exceptions import ManifestNotFoundError, UserAbortedError

logger = logging.getLogger(__name__)


def execute(deps: Dependencies, interactive: bool = True) -> dict:
    """
    Execute install workflow.

    Prompts user to select an asset and version from the repository manifest,
    then installs it locally to NUKE_KIT_DIR and updates the cached manifest.

    Args:
        deps: Injected dependencies containing repository, manifests, and user paths.
        interactive: If True, prompt user for asset and version selection.
            If False, raises NotImplementedError (non-interactive not yet supported).

    Returns:
        Dictionary with 'asset' key containing the installed Asset instance.

    Raises:
        ValueError: If manifests are not loaded.
        UserAbortedError: If user cancels during selection.
        NotImplementedError: If interactive=False (not yet supported).
    """
    if deps.repo_manifest is None or deps.cached_manifest is None:
        raise ManifestNotFoundError("Manifests not loaded")

    # User chooses asset from repository manifest
    if interactive:
        asset = console.choose_asset_fuzzy(
            deps.repo_manifest.to_dict(),
            prompt="Select asset to install",
            prompt_version="Version to install (Latest or specific)",
        )
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
