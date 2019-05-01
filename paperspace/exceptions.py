class ApplicationException(Exception):
    pass


class BadResponseException(ApplicationException):
    pass


class PresignedUrlUnreachableException(ApplicationException):
    pass


class PresignedUrlAccessDeniedException(ApplicationException):
    pass


class PresignedUrlConnectionException(ApplicationException):
    pass


class S3UploadFailedException(ApplicationException):
    pass
