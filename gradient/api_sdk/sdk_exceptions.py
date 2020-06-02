class GradientSdkError(Exception):
    pass


class ResourceFetchingError(GradientSdkError):
    pass


class ResourceCreatingError(GradientSdkError):
    pass


class MalformedResponseError(GradientSdkError):
    pass


class ResourceCreatingDataError(ResourceCreatingError):
    pass


class ArchiveUploadError(GradientSdkError):
    pass


class PresignedUrlMalformedResponseError(ArchiveUploadError):
    pass


class PresignedUrlError(ArchiveUploadError):
    pass


class S3UploadFailedError(ArchiveUploadError):
    pass


class ProjectAccessDeniedError(ArchiveUploadError):
    pass


class ReceivingDataFailedError(ArchiveUploadError):
    pass


class WrongPathError(ArchiveUploadError):
    pass


class PresignedUrlUnreachableError(ArchiveUploadError):
    pass


class PresignedUrlAccessDeniedError(ArchiveUploadError):
    pass


class PresignedUrlConnectionError(ArchiveUploadError):
    pass


class InvalidParametersError(GradientSdkError):
    pass


class EndWebsocketStream(Exception):
    pass
