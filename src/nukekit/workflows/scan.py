from ..core import (
    EnvContext,
    ManifestStore,
    console,
)


def scan_workflow(args, env: EnvContext):
    """
    Scan nuke directory and print available assets to console

    :param context: This sessions"s context
    :type context: EnvContext
    """

    cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)
    local_state_manifest = ManifestStore.load_from_filesystem(
        env.user_paths.NUKE_DIR, cached_manifest
    )
    console.print_data(local_state_manifest.data)
