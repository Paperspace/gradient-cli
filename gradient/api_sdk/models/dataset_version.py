import attr


@attr.s
class DatasetVersionTagSummary(object):
    """
    Dataset version tag summary class
    """
    name = attr.ib(type=str, default=None)


@attr.s
class DatasetVersion(object):
    """
    Dataset version class
    """
    version = attr.ib(type=str, default=None)
    message = attr.ib(type=str, default=None)
    is_committed = attr.ib(type=bool, default=None)
    tags = attr.ib(type=list, factory=list)

    # only used for create
    dataset_id = attr.ib(type=str, default=None)


@attr.s
class DatasetVersionPreSignedS3Call(object):
    """
    Dataset version pre-signed S3 call class
    """
    method = attr.ib(type=str, default=None)
    params = attr.ib(type=dict, factory=dict)


@attr.s
class DatasetVersionPreSignedURL(object):
    """
    Dataset version pre-signed URL class
    """
    url = attr.ib(type=str, default=None)
    expires_in = attr.ib(type=int, default=None)
