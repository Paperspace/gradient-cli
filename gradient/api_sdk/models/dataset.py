import attr


@attr.s
class Dataset(object):
    uri = attr.ib(type=str, default=None)
    aws_access_key_id = attr.ib(type=str, default=None)
    aws_secret_access_key = attr.ib(type=str, default=None)
    etag = attr.ib(type=str, default=None)
    version_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
