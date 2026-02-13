from ..core import (
    EnvContext,
    Manifest,
    Repository,
    console,
)


def scan(args, env: EnvContext):
    """
    Scan nuke directory and print available assets to console

    :param context: This sessions"s context
    :type context: EnvContext
    """

    repo = Repository(env.config)
    repo.add_manifest(Manifest.from_json(repo.MANIFEST_PATH))
    local_manifest = Manifest.from_json(env.user_paths.CACHED_MANIFEST)
    local_state_manifest = Manifest.from_local_state(env.user_paths, local_manifest)
    console.print_data(local_state_manifest.data)
