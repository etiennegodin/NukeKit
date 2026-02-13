from ..core import (
    EnvContext,
    Manifest,
    Repository,
    console,
    scanner,
)


def scan(args, env: EnvContext):
    """
    Scan nuke directory and print available assets to console

    :param context: This sessions"s context
    :type context: EnvContext
    """

    repo = Repository(env.config)
    repo.add_manifest(Manifest.from_json(repo.MANIFEST_PATH))
    local_state_manifest = Manifest.from_local_state(env.user_paths)

    if args.location == "local":
        assets = local_state_manifest.data
    elif args.location == "remote":
        assets = scanner.scan_folder(repo.ROOT)

    console.print_data(assets)
