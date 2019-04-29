class ApplicationException(Exception):
    pass


class BadResponseException(ApplicationException):
    pass


class PresignedUrlUnreachableException(ApplicationException):
    pass


class S3UploadFailedException(ApplicationException):
    pass
