from dotenv import load_dotenv

from ..core import ConfigLoader, ConfigValidator, Context, Repository
from ..utils import UserPaths


def get_context() -> Context:
    """
    Initialize context for this session

    :return: Context instance for current session
    :rtype: Context
    """

    # Load .env
    load_dotenv()

    # Setup user paths
    user_paths = UserPaths()

    # Config solver
    config = ConfigLoader().load()
    ConfigValidator.validate(config)

    # Init Central Repo
    repo = Repository(config)

    # Create and return context instance
    return Context(
        repo,
        user_paths,
        config,
    )
