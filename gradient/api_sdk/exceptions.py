class GradientSdkError(Exception):
    pass


class ResourceFetchingError(GradientSdkError):
    pass


class ResourceCreatingError(GradientSdkError):
    pass
