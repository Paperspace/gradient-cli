class ApplicationError(Exception):
    pass


class BadResponseError(ApplicationError):
    pass


class PresignedUrlUnreachableError(ApplicationError):
    pass


class ProjectAccessDeniedError(ApplicationError):
    pass


class PresignedUrlAccessDeniedError(ApplicationError):
    pass


class PresignedUrlConnectionError(ApplicationError):
    pass


class PresignedUrlMalformedResponseError(ApplicationError):
    pass


class PresignedUrlError(ApplicationError):
    pass


class S3UploadFailedError(ApplicationError):
    pass
