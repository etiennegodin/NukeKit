class NukeKitError(Exception):
    pass


class RepositoryError(NukeKitError):
    pass


class PublishError(NukeKitError):
    pass


class ValidationError(NukeKitError):
    pass


class AssetError(NukeKitError):
    pass
